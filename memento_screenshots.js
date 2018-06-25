/***
Nodejs script to look through each news site's memento.json for a specified date
and then run puppeteer to take screenshots for that date's collected URI-M.
***/

const puppeteer = require('puppeteer');
const fs = require('fs');
const url = require('url');
const crypto = require('crypto');

if (process.argv.length < 4) {
    console.error('Usage: node memento_screenshot.js {DATE(Y-m-d)} {OUT_DIRECTORY}');
    console.error('\nWhen specifiying the date argument remember that the stories were collected from approximately 1AM GMT (8PM ET). \nFor example, December 26, 2016 at 1 AM GMT is actually December 25, 2016 at 8 PM ET.');
    process.exit(1);
}

const memento_dir = "./data/mementos/";
const req_date = new Date(process.argv[2]);
const screenshot_dir = process.argv[3];
const site_mementos = [];

// console.log(req_date);
// console.log(screenshot_dir);

function uriFromHash(hash){
    // helper function to find actual URI given the URI hash
    // sets dictionary default if found
    var hashes = JSON.parse(fs.readFileSync('./data/news-websites-hashes.json'))
    for(var i in hashes){
        if(hashes[i]["hash"] == hash){
            let host = url.parse(hashes[i]["URI-R"]).host;
            site_mementos[host] = {};
            return;
        }
    }
}

function getDirectories(path) {
  return fs.readdirSync(path).filter(function (file) {
    return fs.statSync(path+'/'+file).isDirectory();
  });
}

function parseMementoJSON(mjson){
    // Parse mementos.json from each news site and get the requested URI-M
    // @returns returns URI-M array
    let hashes = getDirectories(memento_dir);
    for(var i in hashes){
        // Format month and day to add 0s
        var month = (1 + req_date.getUTCMonth()).toString();
        month = month.length > 1 ? month : '0' + month;
        var day = req_date.getUTCDate().toString();
        day = day.length > 1 ? day : '0' + day;

        // create path string
        let path = memento_dir + hashes[i] + "/" + req_date.getUTCFullYear() +
                "_" + month + "/mementos.json";
        var obj = JSON.parse(fs.readFileSync(path))

        // Pick out URI-M for memento.json and add to arr
        uriM = obj[hashes[i]][day]["URI-M"];
        site_mementos.push(uriM)
    }
    console.log(site_mementos);
}

async function headless(args) {
    if (!fs.existsSync(screenshot_dir)){
        fs.mkdirSync(screenshot_dir);
    }
    const browser = await puppeteer.launch({
        ignoreHTTPSErrors: true,
        args: args,
        // headless: false,
    });
    for(var i in site_mementos){
        let uriM = site_mementos[i];
        let screenshot = screenshot_dir + "/" + crypto.createHash('md5').update(uriM).digest("hex") + ".png";
        if (fs.existsSync(screenshot)){
            console.log("Skipped:", screenshot);
            continue;
        }
        console.log("Requesting:", uriM);
        const page = await browser.newPage();
        page.emulate({
            viewport: {
                width: 1560,
                height: 1080,
            },
            userAgent: "",
        });

        try {
            // timeout at 60 seconds (6 * 10000ms), network idle at 3 secondsq
            await page.goto(uriM, {
                waitUntil: 'networkidle2',
                timeout: 120000,
            });

            // Take screenshots
            await page.screenshot({
                path: screenshot,
                //fullPage: true
            });

        } catch (e) {
            console.log(uriM,"Failed with error:", e);
            // process.exit(1);
        }
    }
    browser.close();

}

// Execute
parseMementoJSON();
const args = ['--no-sandbox'];
headless(args).then(v => {
    // Once all the async parts finish this prints.
    console.log("Finished Headless");
    process.exit(1);
});
