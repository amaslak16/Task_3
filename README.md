# Task_3

Заготовка Python-проекта. На данный момент в репозитории нет исходного кода,
сторонних зависимостей и тестов. Описание задачи и команды запуска нужно добавить
после появления реализации.

## Подготовка окружения

Локальное окружение проекта использует Python 3.12.

Создайте виртуальное окружение в корне проекта:

```bash
python -m venv .venv
```

Активируйте его:

- Linux / macOS: `source .venv/bin/activate`
- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- Windows cmd: `.venv\Scripts\activate.bat`

В Linux / macOS вместо `python` может потребоваться команда `python3`.
Установка сторонних библиотек пока не требуется.

## Файлы репозитория

- `README.md` — описание проекта и инструкция по публикации.
- `.gitignore` — исключения для виртуального окружения, настроек IDE,
  кешей Python и локальных конфигураций с секретами.
- `.gitattributes` — единые окончания строк текстовых файлов в Git.
- `.editorconfig` — кодировка UTF-8, отступы и настройки пробелов.

## Первая публикация на GitHub

Git уже инициализирован в этой папке. Создайте на GitHub пустой репозиторий
без автоматически создаваемых README, `.gitignore` и лицензии.

Выполните команды из корня проекта, заменив `YOUR_USERNAME` и `YOUR_REPOSITORY`
своим именем пользователя и названием репозитория:

```bash
git add README.md .gitignore .gitattributes .editorconfig
git diff --cached --stat
git commit -m "Prepare repository for GitHub"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Для отправки потребуется авторизация в GitHub. Если Git при создании коммита
сообщает, что имя и почта не настроены, задайте их для этого репозитория
и повторите `git commit`:

```bash
git config user.name "Ваше имя"
git config user.email "your-email@example.com"
```

Когда появятся исходники, добавляйте их в коммит вместе с документацией.
Перед коммитом проверяйте список файлов командой `git status`.

## Лицензия

Лицензия пока не выбрана. При необходимости добавьте файл `LICENSE`
с условиями использования проекта.
