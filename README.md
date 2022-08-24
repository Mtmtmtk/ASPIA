# ASPIA - Acoustic Signal Processing Introductory Application
This application is a part of the MSc project, developed by Motoki Saito, MSc in Audio and Music Technology, University of York.

## What it does

- Allows you to execute acoustic signal processing functions using the [OpenAIR](https://www.openairlib.net/) database.

## What it looks like

![Auralisation](https://github.com/Mtmtmtk/UKDissertation/tree/develop/readmesamples/sample_1.png)
![Impulse Response Analysis](https://github.com/Mtmtmtk/UKDissertation/tree/develop/readmesamples/sample_2.png)
![Spectrogram](https://github.com/Mtmtmtk/UKDissertation/tree/develop/readmesamples/sample_3.png)

## Database

- Database available at [Google Drive](https://drive.google.com/drive/folders/1WnkeMDKhcHAvowOT6f4N4Q2OtaYNGiWu?usp=sharing)
- Place `impulse_response` folder at `/backend/` directory.
- Place the rest of the files at `/frontend/src/assets/` directory.

## Build & Run

0. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)

1. Clone this repository

2. Open `.env` and edit as needed.

3. Build.

```
sudo docker-compose build
```

4. Run.

```
sudo docker-compose up
```
