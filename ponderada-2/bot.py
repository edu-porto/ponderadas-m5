import typer
import inquirer
import time
import pydobot
from serial.tools import list_ports

# Cria uma instância da aplicação
app = typer.Typer()

# Listas as portas seriais disponíveis
available_ports = list_ports.comports()

# Pede para o usuário escolher uma das portas disponíveis
choose_door = inquirer.prompt([
    inquirer.List("porta", message="Escolha a porta serial", choices=[x.device for x in available_ports])
])["porta"]

def process_steps(dados):
    time.sleep(3)
    operacao = dados["operacao"]
    if operacao == "mover":
        return move_robot()
    if operacao == "resetar":
        return reset_robot()
    if operacao == "ligar atuador":
        return turn_on_tool()
    if operacao == "desligar atuador":
        return turn_off_tool()
    if operacao == "posição atual":
        return get_current_position()
    

def move_robot():
    # Cria uma instância do robô
    robo = pydobot.Dobot(port=choose_door, verbose=False)

    # Define a velocidade e a aceleracao do robô
    robo.speed(30, 30)


    while True:
        try:
            x = int(typer.prompt("Digite o primeiro número"))
            y = int(typer.prompt("Digite o segundo número"))
            z = int(typer.prompt("Digite o terceiro número"))
            if x < 200 and y < 200 and z < 200:
                robo.move_to(x, y, z, 39, wait=True)
                return x, y, z

            else:
                print("As coordenadas devem ser menores que 200. Tente novamente por favor")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
        


def reset_robot():
    robo = pydobot.Dobot(port=choose_door, verbose=False)
    # Define a velocidade e a aceleracao do robô
    robo.speed(30, 30)

    # Move o robô para a posição (200, 0, 0)
    robo.move_to(0, 0, 0, 0, wait=True)

def turn_on_tool():
    robo = pydobot.Dobot(port=choose_door, verbose=False)
    robo.suck(True)

def turn_off_tool():
    robo = pydobot.Dobot(port=choose_door, verbose=False)
    robo.suck(False)

def get_current_position():
    robo = pydobot.Dobot(port=choose_door, verbose=False)
    posicao_atual = robo.pose()
    return posicao_atual


@app.command()
def robot():
    while True:  # Keep running indefinitely
        # realiza lista de perguntas para o usuário
        perguntas = [
            inquirer.List("operacao", message="Qual operação deseja realizar?", choices=["ligar atuador", "desligar atuador","posição atual","mover", "resetar","sair"])
        ]



        # realiza a leitura das respostas
        respostas = inquirer.prompt(perguntas)

        # realiza a operação
        saida = process_steps(respostas)

        print(saida)

# Executa a aplicação
if __name__ == "__main__":
    app()
