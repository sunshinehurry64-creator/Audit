import ssl
import socket
import pandas as pd
from cryptography import x509
from datetime import datetime

def audit_quantum_readiness(hostname, port=443):
    """Fungsi utama untuk audit TLS dan PQC Readiness[cite: 469]."""
    results = {
        "hostname": hostname,
        "protocol": None,
        "cipher": None,
        "key_type": None,
        "key_size": None,
        "pqc_status": "BELUM (RSA/ECC)",
        "grade": "C",
        "status": "Success"
    }

    try:
        context = ssl.create_default_context()
        # Mengatur timeout agar pemindaian massal tetap efisien [cite: 489]
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as tls:
                # 1. Ambil info Cipher dan Protokol [cite: 493-500]
                cipher_name, proto_name, bits = tls.cipher()
                results["protocol"] = proto_name
                results["cipher"] = cipher_name

                # 2. Deteksi PQC (Simulasi berdasarkan Cipher Suite) [cite: 435-437, 513]
                pq_keywords = ["kyber", "mlkem", "pq", "hybrid"]
                if any(k in cipher_name.lower() for k in pq_keywords):
                    results["pqc_status"] = "YA (Kyber/Hybrid)"
                    is_pqc = True
                else:
                    is_pqc = False

                # 3. Parsing Sertifikat X.509 [cite: 409-413, 501-511]
                cert_der = tls.getpeercert(binary_form=True)
                cert = x509.load_der_x509_certificate(cert_der)
                pubkey = cert.public_key()
                
                key_type = type(pubkey).__name__
                key_size = getattr(pubkey, "key_size", None)
                results["key_type"] = key_type
                results["key_size"] = key_size

                # 4. Skema Grading Otomatis [cite: 438-468, 516-521]
                is_rsa_strong = "RSA" in key_type.upper() and key_size >= 3072
                is_ec_strong = "EC" in key_type.upper() and key_size >= 256

                if is_pqc and proto_name == "TLSv1.3" and (is_rsa_strong or is_ec_strong):
                    results["grade"] = "A+"
                elif proto_name == "TLSv1.3" and (key_size >= 2048):
                    results["grade"] = "A"
                elif proto_name == "TLSv1.2":
                    results["grade"] = "B"
                else:
                    results["grade"] = "C"

    except Exception as e:
        results["status"] = f"Error: {str(e)}"
    
    return results

# Contoh Penggunaan Massal (100 Domain) [cite: 679]
if __name__ == "__main__":
    target_campis = ["google.com", "itb.ac.id", "ui.ac.id", "unp.ac.id"] # Tambahkan hingga 100
    all_results = [audit_quantum_readiness(host) for host in target_campis]
    df = pd.DataFrame(all_results)
    df.to_csv("hasil_audit_2025.csv", index=False)
    print("Audit Selesai. Data disimpan di hasil_audit_2025.csv")