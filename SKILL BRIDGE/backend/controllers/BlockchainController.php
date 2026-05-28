<?php
/**
 * Blockchain Certificate Handler
 * PHP interface for blockchain operations
 */

class BlockchainCertificateHandler {
    private $python_api_url = 'http://localhost:5000/api/certificate';
    private $db;

    public function __construct($db) {
        $this->db = $db;
    }

    public function createCertificate($user_id, $skill_name, $issuer, $validity_days = 365) {
        /**
         * Create a new digital certificate on blockchain
         */
        $data = [
            'user_id' => $user_id,
            'skill_name' => $skill_name,
            'issuer' => $issuer,
            'validity_days' => $validity_days
        ];

        $certificate = $this->callBlockchainAPI('POST', '/create', $data);

        if (isset($certificate['certificate_hash'])) {
            $this->saveCertificateToDatabase($user_id, $certificate);
        }

        return $certificate;
    }

    public function verifyCertificate($certificate_hash) {
        /**
         * Verify a digital certificate
         */
        $data = ['certificate_hash' => $certificate_hash];
        $verification = $this->callBlockchainAPI('POST', '/verify', $data);

        // Update verification count in database
        if ($verification['is_valid']) {
            $this->updateVerificationCount($certificate_hash);
        }

        return $verification;
    }

    public function getUserCertificates($user_id) {
        /**
         * Get all certificates for a user
         */
        $stmt = $this->db->prepare("SELECT * FROM digital_certificates WHERE user_id = ? AND is_verified = TRUE");
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        return $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
    }

    public function revokeCertificate($certificate_hash, $reason = null) {
        /**
         * Revoke a digital certificate
         */
        $data = [
            'certificate_hash' => $certificate_hash,
            'reason' => $reason
        ];

        $result = $this->callBlockchainAPI('POST', '/revoke', $data);

        if ($result['success']) {
            $stmt = $this->db->prepare("UPDATE digital_certificates SET is_verified = FALSE WHERE certificate_hash = ?");
            $stmt->bind_param("s", $certificate_hash);
            $stmt->execute();
        }

        return $result;
    }

    private function saveCertificateToDatabase($user_id, $certificate) {
        /**
         * Save certificate details to database
         */
        $stmt = $this->db->prepare(
            "INSERT INTO digital_certificates 
            (user_id, skill_name, certificate_hash, blockchain_address, issuer, verification_url, is_verified) 
            VALUES (?, ?, ?, ?, ?, ?, TRUE)"
        );

        $stmt->bind_param(
            "isssss",
            $user_id,
            $certificate['skill_name'],
            $certificate['certificate_hash'],
            $certificate['blockchain_address'],
            $certificate['issuer'],
            $certificate['qr_code_url']
        );

        return $stmt->execute();
    }

    private function updateVerificationCount($certificate_hash) {
        /**
         * Increment certificate verification count
         */
        $stmt = $this->db->prepare("UPDATE digital_certificates SET verification_count = verification_count + 1 WHERE certificate_hash = ?");
        $stmt->bind_param("s", $certificate_hash);
        return $stmt->execute();
    }

    private function callBlockchainAPI($method, $endpoint, $data) {
        /**
         * Call blockchain API (Python backend)
         */
        $url = $this->python_api_url . $endpoint;

        $options = [
            'http' => [
                'method' => $method,
                'header' => 'Content-Type: application/json',
                'content' => json_encode($data),
                'timeout' => 10
            ]
        ];

        $context = stream_context_create($options);
        $response = @file_get_contents($url, false, $context);

        if ($response === false) {
            return ['error' => 'Blockchain service unavailable'];
        }

        return json_decode($response, true);
    }
}
