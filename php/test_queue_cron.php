<?php
// Processa la coda dei test IPTV: appena il test si libera (l'ora del
// cliente precedente è scaduta), genera la linea e la invia
// automaticamente al primo utente in coda.
//
// Da eseguire via cron ogni 5 minuti (il test dura 1 ora):
//   */5 * * * * php /percorso/php/test_queue_cron.php

require __DIR__ . '/config.php';

if (PHP_SAPI !== 'cli') {
    http_response_code(403);
    exit('Forbidden');
}

$database->query("CREATE TABLE IF NOT EXISTS {$table}_test_queue (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userID BIGINT NOT NULL UNIQUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
)");
$database->query("CREATE TABLE IF NOT EXISTS {$table}_test_state (
    id TINYINT NOT NULL PRIMARY KEY,
    holder_userID BIGINT NULL,
    started_at DATETIME NULL
)");
$database->query("INSERT IGNORE INTO {$table}_test_state (id) VALUES (1)");

// Check: il test è ancora preso da un cliente?
$stato = $database->query("SELECT holder_userID, started_at FROM {$table}_test_state WHERE id = 1")->fetch_assoc();
if ($stato && $stato['started_at'] !== null && time() < strtotime($stato['started_at']) + 3600) {
    exit; // occupato, riprova al prossimo giro
}

while (true) {
    $result = $database->query("SELECT q.userID, u.test_iptv
        FROM {$table}_test_queue q
        LEFT JOIN {$table} u ON u.userID = q.userID
        ORDER BY q.created_at ASC, q.id ASC LIMIT 1");
    if (!$result || $result->num_rows == 0) {
        break;
    }
    $row = $result->fetch_assoc();
    $queuedUserID = (int) $row['userID'];

    // Se nel frattempo ha già usato il test mensile, rimuovilo dalla coda
    if ($row['test_iptv'] !== null && (int) $row['test_iptv'] >= 1 && $queuedUserID != 148959990) {
        $database->query("DELETE FROM {$table}_test_queue WHERE userID = $queuedUserID");
        continue;
    }

    $r = new HttpRequest("get", "http://45.86.190.74:81/api/bcc30fb1-3cc1-4cb8-a51a-f91b55f03089/create_test/1");
    $rr = $r->getResponse();
    $ar = json_decode($rr, true);
    if (!is_array($ar) || empty($ar['username']) || empty($ar['password'])) {
        // Il pannello ha rifiutato: riprova al prossimo giro di cron
        break;
    }

    $stmt = $database->prepare("UPDATE {$table}_test_state SET holder_userID = ?, started_at = NOW() WHERE id = 1");
    $stmt->bind_param('i', $queuedUserID);
    $stmt->execute();
    $database->query("UPDATE $table SET test_iptv = test_iptv + 1 WHERE userID = $queuedUserID");
    $database->query("DELETE FROM {$table}_test_queue WHERE userID = $queuedUserID");
    sm($queuedUserID, "✅ <b>Test IPTV disponibile!</b>\n\nIl test si è liberato: ecco la tua linea di test KeTv: " . link_lista($ar['username'], $ar['password']) . "\n\n<i>Ricorda: il test dura 1 ora.</i>");

    // La linea è una sola: dopo averla assegnata torna occupata per 1 ora
    break;
}
