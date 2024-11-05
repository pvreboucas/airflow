# Preparando o ambiente no Ubuntu

```shell
sudo apt update
sudo apt upgrade
sudo apt install build-essential gcc make perl dkms curl tcl
```

## Instalando as bibliotecas Python

Caso você não tenha o python instalado execute os comandos:

```shell
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.9
sudo apt install python3.9-venv
```

Para implementar nosso código, faremos uso de várias bibliotecas Python destacando-se, entre elas, a biblioteca Pandas.

No entanto, antes de procedermos com a instalação dessa biblioteca, precisamos garantir que a ferramenta pip do Python esteja instalada em nosso sistema, pois ela é essencial para instalação de pacotes Python.

Podemos instalar o pip utilizando o seguinte comando:

```shell
sudo apt install python3-pip -y
pip install pandas
```

Para conseguirmos ter acesso a previsão do tempo na cidade de Boston, vamos utilizar uma API chamada Visual Crossing. Com ela, nós podemos fazer até 1000 requisições diárias de forma gratuita e ter acesso a dados passados e futuros em relação ao clima.

## Criando sua conta no site da API

Para começar, podemos acessar o site da API por meio do link da [Visual Crossing](https://www.visualcrossing.com/weather-api). Em seguida, no canto superior direito da tela, podemos clicar em Sign Up para começarmos com a criação da conta gratuita.

## Acessando a chave

Uma vez logado no site, podemos acessar a chave que é gerada para que possamos conseguir trabalhar com os dados fornecidos por essa API. Para acessar essa chave, podemos clicar em Account no canto superior direito da tela.

Em seguida, vamos encontrar nossa chave. Nós podemos clicar no símbolo de uma prancheta localizado ao lado da chave para conseguir copiá-la.