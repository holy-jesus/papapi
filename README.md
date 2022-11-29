# ПАПАПИ ПАПАПА ПАПИПУ
Это бесплатное веб-приложение для генерации дипломов и сертификатов.

Приложение можно использовать здесь: https://papapi.deta.dev/

## Инструкции по разворачиванию:
###  Автоматически:
#### На своём компьютере/:
Просто запустите следующую команду
`
curl -fsSL https://raw.githubusercontent.com/holy-jesus/papapi/main/install.sh | bash
`
Остаётся запустить приложение командой:
`
./run.sh
`
И перейти по ссылке http://localhost:5000/
#### Способ 2:
Задеплойить свою версию на Deta:
[![Deploy](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy?repo=https://github.com/holy-jesus/papapi)
### Вручную:
1. Установите Python и git
`
sudo apt install python3 python3-pip python3-venv git
`
2. Склонируйте репозиторий с помощью команды
`
git clone https://github.com/holy-jesus/papapi.git && cd ./papapi/
`
3. В папке репозитория создайте виртуальную среду разработки
`
python3 -m venv ./venv/
`
4. Установите необходимые модули с помощью команды
`
pip3 install -r requirements.txt
`
5. Запустите сайт
`
python3 main.py
`
6. Чтобы зайти на сайт надо перейти по ссылке http://localhost:5000/
