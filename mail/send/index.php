<?php
header('Content-Type: application/json');

// Catch any fatal errors and return JSON instead of HTML
register_shutdown_function(function () {
    $error = error_get_last();
    if ($error && in_array($error['type'], [E_ERROR, E_PARSE, E_CORE_ERROR, E_COMPILE_ERROR])) {
        if (!headers_sent()) http_response_code(500);
        echo json_encode(['success' => false, 'message' => 'Server error: ' . $error['message']]);
    }
});

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;
use PHPMailer\PHPMailer\SMTP;

require_once '../../vendor/autoload.php';

$dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
$dotenv->safeLoad();

// Check if the request method is POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Only POST requests are allowed']);
    exit;
}

// Check if the content type is JSON
if (strpos($_SERVER['CONTENT_TYPE'] ?? '', 'application/json') === false) {
    http_response_code(415);
    echo json_encode(['error' => 'Content type must be application/json']);
    exit;
}

// Get the JSON input
$input = json_decode(file_get_contents('php://input'), true);

if (!$input) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON input']);
    exit;
}

// Check if the token is present and valid
$validToken = $_ENV['SECRET_TOKEN'] ?? '';
$headers = getallheaders();
if (!isset($headers['Token']) || $headers['Token'] !== $validToken) {
    http_response_code(401);
    echo json_encode(['error' => 'Invalid or missing token']);
    exit;
}

$mail = new PHPMailer(true);

try {
    //Server settings
    $mail->SMTPDebug = SMTP::DEBUG_OFF;                                       // Enable verbose debug output
    $mail->isSMTP();                                            // Set mailer to use SMTP
    $mail->Host       = $_ENV['SMTP_HOST'];                    // Specify main and backup SMTP servers
    $mail->SMTPAuth   = true;                                   // Enable SMTP authentication
    $mail->Username   = $_ENV['SMTP_USERNAME'];                // SMTP username
    $mail->Password   = $_ENV['SMTP_PASSWORD'];                // SMTP password
    $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;         // Enable TLS encryption, `ssl` also accepted
    $mail->Port       = $_ENV['SMTP_PORT'];                    // TCP port to connect to

    //Recipients
    $mail->setFrom($_ENV['MAIL_FROM_ADDRESS']);
    $mail->addAddress('developer@agilecyber.com');           // Add a recipient
    // $mail->addReplyTo('info@example.com', 'Information');

    // Content
    $mail->isHTML(true);                                        // Set email format to HTML
    $mail->Subject = 'New Contact Form Submission';
    $mail->Body    = 'You have received a new message from your website contact form.<br><br>' .
                     '<b>First Name:</b> ' . htmlspecialchars($input['firstName'] ?? '') . '<br>' .
                     '<b>Last Name:</b> '  . htmlspecialchars($input['lastName']  ?? '') . '<br>' .
                     '<b>Email:</b> '      . htmlspecialchars($input['email']     ?? '') . '<br>' .
                     '<b>Message:</b> '    . nl2br(htmlspecialchars($input['message'] ?? '')) . '<br>';
    $mail->AltBody = 'You have received a new message from your website contact form.' . "\n\n" .
                     'First Name: ' . htmlspecialchars($input['firstName'] ?? '') . "\n" .
                     'Last Name: '  . htmlspecialchars($input['lastName']  ?? '') . "\n" .
                     'Email: '      . htmlspecialchars($input['email']     ?? '') . "\n" .
                     'Message: '    . htmlspecialchars($input['message']   ?? '');

    $mail->send();

    http_response_code(200);
    echo json_encode(['success' => true, 'message' => 'Message has been sent']);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Something went wrong!', 'error' => "Message could not be sent. Mailer Error: {$mail->ErrorInfo}"]);
}