# Mail Atomata

A stable and reliable email automation tool based on `message broker` service architecture.

## Tech Stack:

- Django
- Celery
- MySQL
- Docker
- RabbitMQ

### Highlights:

- Upload the data as `CSV` file which contains the columns **Name** and **Email**.
- Secret key based authentication
- Single Management Console
- Multithreaded workers for faster performance

### Run:

- Clone the repository :  
  `git pull https://github.com/nav-sk/MailAtomata.git`

- Follow the `.env.template` file and make your own `.env`.

- Up the containers : `docker compose up`
