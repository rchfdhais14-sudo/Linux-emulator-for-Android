import os
import sys
import subprocess
import threading

def read_output(process):
    """Этот поток непрерывно читает ответы от ядра Linux 🐧"""
    while True:
        # Читаем по одному байту, чтобы текст выводился мгновенно
        char = process.stdout.read(1)
        if not char:
            break
        sys.stdout.write(char)
        sys.stdout.flush()

def start_linux_bridge_fixed():
    print("\033[1;33m" + "="*50 + "\033[0m")
    print("\033[1;36m🛸 ЗАПУСК СВЕРХПРОЧНОГО МОСТА LINUX... 🛸\033[0m")
    print("\033[1;32mОбходим блокировки pty через прямые потоки ядра. \033[0m")
    print("\033[1;33m" + "="*50 + "\033[0m\n")

    # Системный шелл Android (настоящий Linux внутри телефона) 🤖
    shell = "/system/bin/sh"
    
    # Настраиваем окружение
    env = os.environ.copy()
    env["PATH"] = "/system/bin:/system/xbin:/sbin:" + env.get("PATH", "")

    # Запускаем настоящий системный процесс Linux через сквозные пайпы!
    process = subprocess.Popen(
        [shell],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, # Объединяем ошибки и обычный вывод
        env=env,
        text=True, # Работаем сразу с текстом, а не с байтами
        bufsize=0  # Отключаем буферизацию для мгновенного ответа
    )

    # Запускаем фоновый поток, который будет ловить ответы от Linux 🧵
    t = threading.Thread(target=read_output, args=(process,), daemon=True)
    t.start()

    print("\033[1;32m✅ МОСТ НАПРЯМУЮ СВЯЗАН С ЯДРОМ! Вводи команды ниже: \033[0m")
    print("(Подсказка: начни с команд: 'ls', 'pwd' или 'uname -a')\n")

    # Цикл отправки команд пользователя в ядро 🔄
    while process.poll() is None:
        try:
            # Считываем то, что ты ввел в Pydroid 3
            user_command = input().strip()
            if user_command.lower() == "exit":
                break
            
            # Отправляем команду в ядро и добавляем перенос строки \n
            process.stdin.write(user_command + "\n")
            process.stdin.flush()
            
        except (KeyboardInterrupt, EOFError):
            break

    print("\n\033[1;31m🛑 Мост с ядром Linux успешно закрыт.\033[0m")

if __name__ == "__main__":
    start_linux_bridge_fixed()
