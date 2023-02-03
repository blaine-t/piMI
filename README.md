<p align="center">
  <img src="/dev/img/PiMI256.png" height="128">
</p>

## Description

piMI is a low cost server management interface made with the Raspberry Pi Pico W. Includes support for optional e-ink display. Supports power management and real time system information from anywhere with WebSockets. 

## Powered By

### Frontend:
      <img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/logos/exports/1544x1544_circle.png" height="20"> [**Catppuccin**](https://github.com/catppuccin/catppuccin) - used for the color scheme, it is pleasing and dark, with good guidelines on how to implement it <br />
      <img src="https://www.chartjs.org/img/chartjs-logo.svg" height="20"> [**Chart.js**](https://www.chartjs.org) - used to create the graphs in the web interface <br />
      <img src="https://avatars.githubusercontent.com/u/678099" height="20"> [**Numeral.js**](https://github.com/adamwdraper/Numeral-js) - used to abbreviate large numbers on the charts <br />

### Backend: 
      <img src="https://about.gitlab.com/images/press/logo/svg/gitlab-logo-500.svg" height="20"> [**raspberry_pico_w_websocket**](https://gitlab.com/florindragan/raspberry_pico_w_websocket) - Very important baseline for websockets for serving to web clients <br />
      <img src="https://avatars.githubusercontent.com/u/3429760" height="20"> [**dool**](https://github.com/scottchiefbaker/dool) - Useful for getting system statistics easily sent to the pi <br />
      <img src="https://www.waveshare.com/w/upload/a/a7/Ws-watermark-en.svg" height="20"> [**Waveshare Library**](https://github.com/waveshare/Pico_ePaper_Code) - Waveshare (incomplete and not documented) e-ink library <br />

## Special Thanks To

      <img src="https://play-lh.googleusercontent.com/2GLTIKKy3rGhM1qJv12K3EX7ZtJW2fVWf-SIYawtA9OXbo3gSDudEdHIO4i_MFyOek0" height="20"> [**Digikey Async Guide**](https://www.digikey.com/en/maker/projects/getting-started-with-asyncio-in-micropython-raspberry-pi-pico/110b4243a2f544b6af60411a85f0437c) - Allowed us to learn how to do async code faster and properly. <br />
      <img src="https://styles.redditmedia.com/t5_mjvcg/styles/profileIcon_snoo16d1b197-7907-4b95-a9ce-e1a0f691c9bd-headshot.png" height="20"> [**u/Zachmarius**](https://www.reddit.com/user/Zachmarius/) - for E-ink landscape support, very useful and saved a lot of work. <br />
      <img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Micropython-logo.svg" height ="20"> [**Roberth & jdts**](https://forum.micropython.org/viewtopic.php?t=7325) - The non-blocking serial code proved very important in recieving data from the host computer. <br />

## Contributors

      <img src="https://avatars.githubusercontent.com/u/72430668" height="20"> [**G2-Games**](https://github.com/G2-Games) - Frontend Dev <br />
      <img src="https://avatars.githubusercontent.com/u/108963625" height="20"> [**blaine-t**](https://github.com/blaine-t) - Backend Dev
