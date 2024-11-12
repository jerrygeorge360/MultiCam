# Multi-Camera Twitch Viewer App

> **Tagline**: **Stream. Switch. Enjoy.**

This project is a dynamic multi-angle camera viewer for Twitch, where viewers can seamlessly switch between camera angles while watching live streams. The streamer sets up multiple cameras, and viewers can control which angle they want to see in real-time, enhancing their engagement and viewing experience.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Future Enhancements](#future-enhancements)

## Overview

The Multi-Camera Twitch Viewer App allows viewers to choose their preferred camera angle on a live Twitch stream. It is designed to create an immersive, customizable viewing experience, where the audience has control over which camera angle they want to watch. This is achieved by streaming a default camera angle to Twitch while managing additional angles on a separate media server.

## Features

- **Multi-Angle Viewing**: Viewers can switch between different camera angles during a live stream.
- **Twitch Authentication**: Allows streamers to register with their Twitch accounts and for viewers to sign in to access enhanced features.
- **Followed Streamers**: Viewers can quickly find and access camera angles for streamers they follow.
- **Custom Media Server Integration**: Additional camera streams are hosted on a media server, allowing smooth switching for viewers.
- **Neomorphic and Cyberpunk UI**: Minimalistic, immersive design with a futuristic touch.

## How It Works

### For Streamers
1. **Register with Twitch**: Streamers authenticate using their Twitch account.
2. **Set Up Cameras**: Streamers set up multiple camera angles, streaming the default angle to Twitch and other angles to a media server.
3. **Stream Control**: The app automatically configures the streams for the viewers to select.

### For Viewers
1. **Log In and Follow**: Viewers can log in with their Twitch accounts and access a list of followed streamers or global streamers registered in the app with available multi-angle streams.
2. **Dynamic Camera Switching**: From the viewer interface, they can switch between available camera angles during a live stream.
3. **Personalized Experience**: Viewers enjoy a customizable viewing experience through an easy-to-use interface.


## Tech Stack

- **Frontend**: HTML, SCSS (with a neomorphic and cyberpunk minimalistic design), JavaScript
- **Backend**: python,flask,postgresql
- **Authentication**: Twitch OAuth
- **Media Server**: Wowza Streaming Engine
- **Video Player**: Custom WebRTC player integrated with Wowza

## Future Enhancements

- **Advanced Analytics**: Provide streamers with analytics on which camera angles are popular among viewers.
- **Viewer Interaction Tools**: Enable chat or poll features for real-time viewer interaction.
- **UI improvements**: