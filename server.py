import socket
import threading
import time
import os

def handle_udp_ping(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            sock.sendto(data, addr)
        except Exception as e:
            print(f"Erreur UDP: {e}")
            break

def handle_tcp_client(conn, addr):
    print(f"Connexion TCP de {addr}")
    conn.settimeout(20)  # Timeout de 20 secondes

    # Désactiver Nagle's Algorithm
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    # Augmenter les tailles de buffer des sockets
    buffer_size = 1048576  # 1 Mo
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size)
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, buffer_size)

    try:
        data = conn.recv(1024).decode().strip()
        if data == "START_DOWNLOAD":
            conn.sendall(b"OK\n")
            print(f"Début du test de téléchargement pour {addr}")
            start_time = time.time()
            data_sent = 0
            payload = os.urandom(buffer_size)  # Données aléatoires
            while True:
                try:
                    conn.sendall(payload)
                    data_sent += len(payload)
                    # Vérifier si le client a envoyé le signal de fin
                    conn.settimeout(0.1)
                    try:
                        end_signal = conn.recv(1024)
                        if b"END_TEST" in end_signal:
                            break
                    except socket.timeout:
                        pass  # Pas de données reçues, continuer
                    conn.settimeout(None)
                except BrokenPipeError:
                    print(f"Le client {addr} a fermé la connexion.")
                    break
                except Exception as e:
                    print(f"Erreur lors de l'envoi à {addr}: {e}")
                    break
            duration = time.time() - start_time
            print(f"Test de téléchargement terminé pour {addr}. Données envoyées: {data_sent / (1024*1024):.2f} Mo en {duration:.2f} secondes")

        elif data == "START_UPLOAD":
            conn.sendall(b"OK\n")
            print(f"Début du test de téléversement pour {addr}")
            start_time = time.time()
            data_received = 0
            while True:
                try:
                    chunk = conn.recv(buffer_size)
                    if not chunk:
                        break
                    if b"END_TEST" in chunk:
                        break
                    data_received += len(chunk)
                except socket.timeout:
                    break
                except Exception as e:
                    print(f"Erreur lors de la réception de {addr}: {e}")
                    break
            duration = time.time() - start_time
            print(f"Test de téléversement terminé pour {addr}. Données reçues: {data_received / (1024*1024):.2f} Mo en {duration:.2f} secondes")
    except Exception as e:
        print(f"Erreur avec {addr}: {e}")
    finally:
        conn.close()
        print(f"Connexion fermée avec {addr}")

def start_server(host='0.0.0.0', tcp_port=5000, udp_port=5000):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((host, udp_port))
    udp_thread = threading.Thread(target=handle_udp_ping, args=(udp_sock,))
    udp_thread.daemon = True
    udp_thread.start()

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sock.bind((host, tcp_port))
    tcp_sock.listen(20)

    print(f"Le serveur écoute sur {host}:{tcp_port} (TCP) et {udp_port} (UDP)")

    try:
        while True:
            conn, addr = tcp_sock.accept()
            threading.Thread(target=handle_tcp_client, args=(conn, addr)).start()
    except KeyboardInterrupt:
        print("Arrêt du serveur demandé par l'utilisateur")
    finally:
        tcp_sock.close()
        udp_sock.close()

if __name__ == "__main__":
    start_server()
