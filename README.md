# Desafio Pong - 2021.1

## Introdução
![banner](/resources/logo.png)

## Organização
O projeto contém 3 pacotes:

- `camera_info` - Pacote desenvolvido para capturar os dados das cameras e publicá-los em um tópico acessível para as demais instâncias do projeto.

- `body_tracking` - Este pacote é responsável por processar as imagens e detectar as partes de corpos de pessoas.
  
- `3d_mapping` - Pacote desenvolvido para processar as imagens das duas câmeras e fazer um mapeamento 3D a partir delas.


### Pré-requisitos 
Para conseguir rodar o map no seu computador você precisa ter um sistema operacional linux com o ROS Noetic instalado.

### Instalação
Siga os seguintes comandos para instalar os pacotes do map no seu computador.

```
$ mkdir -p ~/mapvision_ws/src
$ cd ~/mapvision_ws/src
$ git clone https://github.com/rascimatec/mapvision.git
$ cd .. && catkin_make
``` 
## Como utilizar o Map
Aqui você irá encontrar como utilizar o mapvision e seus pacotes individualmente.

### Carregando os pacotes do Map
Está fase ainda está em desenvolvimento.


## Desenvolvimento

## Equipe

**João Pedro**
<!-- - Email: alexandre.s@aln.senaicimatec.edu.br
- GitHub: https://github.com/Alexandreaags -->

**Marcos Caíque**
<!-- - Email: joao.calmon@aln.senaicimatec.edu.br
- GitHub: https://github.com/GabrielCalmon
- Lattes: http://lattes.cnpq.br/3714599132684846 -->

**Vitor Mendes**
- Email: vitor.mendes@ieee.org
- GitHub: https://github.com/vitorsmends
- Lattes: http://lattes.cnpq.br/1253937974490834
- LinkedIn: https://www.linkedin.com/in/vitorsmends

*“Intelligence is not a privilege, it’s a gift. And you use it for the good of mankind.”* ― Dr. Otto Octavius, Spider-Man 2(2004).

## References

