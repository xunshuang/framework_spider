#!/usr/bin/env bash

ps aux |grep python3 | grep "Crawler" | awk '{print $2}' | xargs kill -9