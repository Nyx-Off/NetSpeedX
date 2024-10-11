import socket
import time
import struct
import threading
import queue
import os

IP_SERVER = "ip_de_votre_server"

def mesure_latence(host= IP_SERVER, port=5000, essais=10):
    latences = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    for _ in range(essais):
        try:
            start = time.time()
            sock.sendto(b'ping', (host, port))
            data, _ = sock.recvfrom(1024)
            end = time.time()
            latence = (end - start) * 1000
            latences.append(latence)
        except socket.timeout:
            print("Timeout lors de la mesure de latence")
    sock.close()
    return min(latences) if latences else None

def worker(q, host, port, direction, duration, event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)  # Timeout de 10 secondes pour la connexion

    # Désactiver Nagle's Algorithm
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    # Augmenter les tailles de buffer des sockets
    buffer_size = 1048576  # 1 Mo
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, buffer_size)

    try:
        sock.connect((host, port))

        if direction == "down":
            sock.sendall(b"START_DOWNLOAD\n")
        else:
            sock.sendall(b"START_UPLOAD\n")

        # Attendre la réponse OK du serveur
        response = b""
        start_time = time.time()
        while b"OK\n" not in response:
            chunk = sock.recv(1024)
            if not chunk:
                raise ConnectionError("Connexion fermée par le serveur")
            response += chunk
            if time.time() - start_time > 5:
                raise ConnectionError("Timeout en attendant la réponse du serveur")

        # Démarrer le test
        start_time = time.time()
        data_transferred = 0
        payload = os.urandom(buffer_size)  # Données aléatoires

        if direction == "down":
            while time.time() - start_time < duration and not event.is_set():
                data = sock.recv(buffer_size)
                if not data:
                    break
                data_transferred += len(data)
        else:
            while time.time() - start_time < duration and not event.is_set():
                sent = sock.send(payload)
                data_transferred += sent
                if sent == 0:
                    break

        # Envoyer un message de fin de test
        sock.sendall(b"END_TEST\n")

    except Exception as e:
        print(f"Erreur dans le thread de test : {e}")
    finally:
        sock.close()

    q.put(data_transferred)

def mesure_debit(host=IP_SERVER, port=5000, duree=15, direction="down", threads=16):
    q = queue.Queue()
    event = threading.Event()
    thread_list = []

    for _ in range(threads):
        t = threading.Thread(target=worker, args=(q, host, port, direction, duree, event))
        t.start()
        thread_list.append(t)

    try:
        for t in thread_list:
            t.join(timeout=duree + 5)  # Attendre un peu plus que la durée prévue
    except KeyboardInterrupt:
        print("Test interrompu par l'utilisateur")
    finally:
        event.set()  # Signaler à tous les threads de s'arrêter

    total_transferred = 0
    while not q.empty():
        total_transferred += q.get()

    debit = (total_transferred * 8) / duree / (1024 * 1024)  # Mbps
    return debit

if __name__ == "__main__":
    print("Début des tests de performance réseau...")

    print("Test de latence...")
    latence = mesure_latence()

    print("Test de débit descendant...")
    debit_descendant = mesure_debit(direction="down")

    print("Test de débit montant...")
    debit_montant = mesure_debit(direction="up")

    if latence is not None:
        print(f"Latence: {latence:.2f} ms")
    else:
        print("Latence: échec de la mesure")

    print(f"Débit descendant: {debit_descendant:.2f} Mbps")
    print(f"Débit montant: {debit_montant:.2f} Mbps")

    print("Tests terminés.")
