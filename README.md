# ![piMI](/dev/img/PiMI256.png)

## Description

piMI is a low cost server management interface made with the Raspberry Pi Pico W. Includes support for optional e-ink display. Supports power management and real time system information from anywhere with WebSockets. 

## Powered By

- <img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/logos/exports/1544x1544_circle.png" height="20"> [**Catppuccin**](https://github.com/catppuccin/catppuccin) - used for the color scheme, it is pleasing and dark, with good guidelines on how to implement it.
- <img src="https://www.chartjs.org/img/chartjs-logo.svg" height="20"> [**Chart.js**](https://www.chartjs.org) - used to create the graphs in the web interface
- <img src="https://styles.redditmedia.com/t5_mjvcg/styles/profileIcon_snoo16d1b197-7907-4b95-a9ce-e1a0f691c9bd-headshot.png" height="20">[**Waveshare Library**](https://www.reddit.com/r/raspberry_pi/comments/10feijl/comment/j56vb2m/?utm_source=share&utm_medium=web2x&context=3) - Waveshare e-ink library modified by [u/Zachmarius](https://www.reddit.com/user/Zachmarius/) for landscape, very useful and saved a lot of work.

## TODO:

- [ ] Display (Style graphics and get partial refresh working in landscape)
- [x] HTML (Add graphs and other elements)
- [x] CSS (Style page)
- [ ] JS (Properly send data to graphs (Update to support doughnut and bar charts))
- [ ] Physically wire up LED pwr and rst switches
- [ ] Install pi and display in case
- [ ] Create USB internal cable
