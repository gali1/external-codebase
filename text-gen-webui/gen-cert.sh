#!/bin/bash

# Generate a self-signed SSL certificate and key with wildcard domain

CERT_FILE="cert.pem"
KEY_FILE="key.pem"
DAYS=365  # Validity period of the certificate in days

# Generate private key
openssl genrsa -out $KEY_FILE 2048

# Create a temporary config file for the CSR and certificate
cat > cert_config.cnf <<EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
req_extensions = req_ext
distinguished_name = dn

[dn]
CN = *.gademo.net

[req_ext]
subjectAltName = @alt_names

[alt_names]
DNS.1 = *.gademo.net
EOF

# Generate certificate signing request (CSR) using the private key
openssl req -new -key $KEY_FILE -out $CERT_FILE.csr -config cert_config.cnf

# Generate self-signed certificate using the private key
openssl x509 -req -in $CERT_FILE.csr -signkey $KEY_FILE -out $CERT_FILE -days $DAYS -extensions req_ext -extfile cert_config.cnf

# Cleanup temporary files
rm $CERT_FILE.csr cert_config.cnf

echo "Self-signed SSL certificate ($CERT_FILE) and key ($KEY_FILE) with wildcard domain (*.gademo.net) generated successfully."
