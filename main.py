import os
import hashlib
import json
import shutil
import subprocess

# Caminhos fixos
XAMPP_PATH = r'C:\xampp'
BACKUP_PATH = r'C:\xampp_backup'
HASHES_FILE = 'hashes.json'

# ===== Funções =====


def calcular_hash(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for bloco in iter(lambda: f.read(4096), b''):
            sha256.update(bloco)
    return sha256.hexdigest()


def gerar_hashes():
    print("Gerando hashes dos arquivos de C:\\xampp...")
    hashes = {}

    for root, dirs, files in os.walk(XAMPP_PATH):
        for file in files:
            caminho_absoluto = os.path.join(root, file)
            caminho_relativo = os.path.relpath(caminho_absoluto, XAMPP_PATH)
            try:
                hash_arquivo = calcular_hash(caminho_absoluto)
                hashes[caminho_relativo.replace("\\", "/")] = hash_arquivo
                print(f"✔️  {caminho_relativo}")
            except Exception as e:
                print(f"[ERRO] {caminho_relativo}: {e}")

    with open(HASHES_FILE, "w") as f:
        json.dump(hashes, f, indent=4)
    print(f"\n✅ Arquivo '{HASHES_FILE}' gerado com sucesso.\n")


def criar_backup():
    if os.path.exists(BACKUP_PATH):
        print(f"🛈 A pasta de backup já existe em {BACKUP_PATH}")
        resposta = input("Deseja sobrescrever o backup? (s/n): ").strip().lower()
        if resposta != 's':
            print("Operação cancelada.\n")
            return
    try:
        shutil.copytree(XAMPP_PATH, BACKUP_PATH, dirs_exist_ok=True)
        print(f"\n✅ Backup criado com sucesso em {BACKUP_PATH}\n")
    except Exception as e:
        print(f"[ERRO] Falha ao criar backup: {e}")


def verificar_integridade():
    print("🔍 Verificando integridade dos arquivos...\n")
    erros = []

    if not os.path.exists(HASHES_FILE):
        print(f"[ERRO] Arquivo de hashes '{HASHES_FILE}' não encontrado. Gere-o primeiro.\n")
        return

    with open(HASHES_FILE, 'r') as f:
        arquivos_esperados = json.load(f)

    for arquivo, hash_esperado in arquivos_esperados.items():
        caminho_completo = os.path.join(XAMPP_PATH, arquivo)
        if not os.path.exists(caminho_completo):
            erros.append((arquivo, 'ARQUIVO AUSENTE'))
            print(f"[ERRO] {arquivo} está faltando.")
            continue
        hash_atual = calcular_hash(caminho_completo)
        if hash_atual != hash_esperado:
            erros.append((arquivo, 'HASH INCORRETO'))
            print(f"[ERRO] {arquivo} está corrompido ou foi alterado.")
        else:
            print(f"[OK] {arquivo}")

    if not erros:
        print("\n✅ Todos os arquivos estão íntegros.\n")
    else:
        print("\n⚠️ Erros encontrados:")
        for arquivo, tipo in erros:
            print(f" - {arquivo}: {tipo}")

        corrigir = input("\nDeseja tentar corrigir usando o backup? (s/n): ").strip().lower()
        if corrigir == 's':
            corrigir_erros(erros)


def corrigir_erros(erros):
    for arquivo, tipo in erros:
        origem = os.path.join(BACKUP_PATH, arquivo)
        destino = os.path.join(XAMPP_PATH, arquivo)
        if os.path.exists(origem):
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.copy2(origem, destino)
            print(f"[CORRIGIDO] {arquivo}")
        else:
            print(f"[FALHA] Backup ausente para: {arquivo}")


# ===== Função para verificar a porta 3306 =====

def verificar_porta_ocupada():
    # Usando netstat para verificar se a porta 3306 está ocupada
    comando = 'netstat -ano | findstr :3306'
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)

    if resultado.stdout:
        # A porta está ocupada, captura o PID
        linhas = resultado.stdout.strip().split('\n')
        for linha in linhas:
            partes = linha.split()
            pid = partes[-1]  # PID do processo que usa a porta
            print(f"🔴 Porta 3306 está ocupada pelo processo com PID {pid}")

            # Verifica qual processo está usando essa porta
            comando_processo = f'tasklist /fi "PID eq {pid}"'
            processo = subprocess.run(comando_processo, shell=True, capture_output=True, text=True)

            if processo.stdout:
                print(f"Processo ocupando a porta 3306: {processo.stdout}")
                encerrar = input("\nDeseja encerrar este processo? (s/n): ").strip().lower()
                if encerrar == 's':
                    # Encerrar o processo
                    subprocess.run(f'taskkill /PID {pid} /F', shell=True)
                    print(f"✅ Processo {pid} encerrado com sucesso.\n")
            else:
                print("[ERRO] Não foi possível identificar o processo.")
    else:
        print("✅ Porta 3306 está livre.\n")


# ===== Menu principal =====
def menu():

    while True:

        print("\n=== Menu de Verificação XAMPP ===")
        print("1. Gerar arquivo de hashes (hashes.json)")
        print("2. Criar/atualizar backup da pasta C:\\xampp")
        print("3. Verificar integridade dos arquivos")
        print("4. Verificar se a porta 3306 está ocupada")
        print("5. Sair")
        escolha = input("Escolha uma opção (1-5): ").strip()

        if escolha == '1':
            gerar_hashes()
        elif escolha == '2':
            criar_backup()
        elif escolha == '3':
            verificar_integridade()
        elif escolha == '4':
            verificar_porta_ocupada()
        elif escolha == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


# Executa o menu
if __name__ == "__main__":
    menu()
