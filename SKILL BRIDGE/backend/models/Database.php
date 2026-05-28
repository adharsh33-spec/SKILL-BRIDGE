<?php
/**
 * Database Connection Handler
 * Establishes MySQL connection with error handling
 */

class Database {
    private $host = DB_HOST;
    private $db_name = DB_NAME;
    private $user = DB_USER;
    private $password = DB_PASSWORD;
    private $port = DB_PORT;
    private $conn;

    public function connect() {
        $this->conn = new mysqli($this->host, $this->user, $this->password, $this->db_name, $this->port);

        if ($this->conn->connect_error) {
            die('Connection Failed: ' . $this->conn->connect_error);
        }

        $this->conn->set_charset("utf8");
        return $this->conn;
    }

    public function query($sql) {
        return $this->conn->query($sql);
    }

    public function prepare($sql) {
        return $this->conn->prepare($sql);
    }

    public function escape_string($string) {
        return $this->conn->real_escape_string($string);
    }

    public function close() {
        if ($this->conn) {
            $this->conn->close();
        }
    }

    public function getLastId() {
        return $this->conn->insert_id;
    }

    public function getAffectedRows() {
        return $this->conn->affected_rows;
    }
}
