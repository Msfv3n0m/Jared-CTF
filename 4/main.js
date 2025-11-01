const express = require('express');
const app = express();
app.use(express.json());
var _ = require('lodash');
const fs = require('fs');
const path = require('path');

const defaultSettings = {
  theme: {
    color: "blue",
    font: "Arial"
  },
  notifications: {
    email: true,
    sms: false
  }
};

app.use(express.json());

app.post('/', (req, res) => {
    const savedSettings = fs.readFile('settings.json', 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading file:', err);
        return {};
    }
});

    if (!req.is('application/json')) {
        res.status(415).json({error: 'content type must be json'});
    }
    const newSettings = req.body;

    if (!newSettings.hasOwnProperty('theme')) {
        res.status(400).json({ error: 'Theme settings are required.' });
    }

    if (!newSettings.hasOwnProperty('notifications')) {
        res.status(400).json({ error: 'Notifications settings are required.' });
    }

    const finalSettings = _.merge({}, savedSettings, newSettings);
    fs.writeFile('settings.json', JSON.stringify(finalSettings, null, 2), 'utf8', (err) => {
    if (err) {
        console.error('Error writing file:', err);
    } else {
        console.log('File saved!');
    }
    });

    res.json(finalSettings);
});

fs.access('settings.json', fs.constants.F_OK, (err) => {
  if (err) {
    fs.writeFile('settings.json', JSON.stringify(defaultSettings, null, 2), 'utf8', (err) => {
      if (err) {
        console.error('Error creating default settings.json file:', err);
      } else {
        console.log('settings.json created successfully');
      }
    });
  } else {
    console.log('settings.json already exists');
  }
});

const colorize = (...args) => ({
  black: `\x1b[30m${args.join(' ')}`,
  red: `\x1b[31m${args.join(' ')}`,
  green: `\x1b[32m${args.join(' ')}`,
  yellow: `\x1b[33m${args.join(' ')}`,
  blue: `\x1b[34m${args.join(' ')}`,
  magenta: `\x1b[35m${args.join(' ')}`,
  cyan: `\x1b[36m${args.join(' ')}`,
  white: `\x1b[37m${args.join(' ')}`,
  bgBlack: `\x1b[40m${args.join(' ')}\x1b[0m`,
  bgRed: `\x1b[41m${args.join(' ')}\x1b[0m`,
  bgGreen: `\x1b[42m${args.join(' ')}\x1b[0m`,
  bgYellow: `\x1b[43m${args.join(' ')}\x1b[0m`,
  bgBlue: `\x1b[44m${args.join(' ')}\x1b[0m`,
  bgMagenta: `\x1b[45m${args.join(' ')}\x1b[0m`,
  bgCyan: `\x1b[46m${args.join(' ')}\x1b[0m`,
  bgWhite: `\x1b[47m${args.join(' ')}\x1b[0m`
});

fs.readFile("README","utf8" ,function(err, contents){
  console.log(colorize('GOAL: ' + contents).green); 
  console.log(colorize('').white); 
});

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
});
