const fs = require('fs');

const EXAMINED_FILE = './examined.lst';
const URL_FILE = './urls.lst';

var data = '';

process.stdin.resume();
process.stdin.setEncoding('utf8');

process.stdin.on('data', function(chunk) {
  data += chunk;
});

process.stdin.on('end', function() {
  processFileList(
    data.split("\n").filter(_=> _)
  );
});

function processFileList(files) {
  const examinedFiles = contentToArray(open(EXAMINED_FILE));
  console.log('Already examined:', examinedFiles, examinedFiles.length);


  files = files.filter((file) => examinedFiles.indexOf(file) === -1);
  console.log('Will examine:', files, files.length);

  const urls = files
    .map((file) => open(file))
    .map(findURLs)
    .reduce((a, b) => a.concat(b), [])
    .filter(_ => _)
    .map((url) => 'https://web.archive.org' + url);
  console.log('Found URLS:', urls, urls.length);

  const existing_urls = contentToArray(open(URL_FILE));
  writeTo(URL_FILE, unique(existing_urls.concat(urls)));
  writeTo(EXAMINED_FILE, unique(examinedFiles.concat(files)));
  console.log('Recorded files');
}

const ourTeamRegExp = /\/web\/([0-9]+)\/http:\/\/www\.freshbooks\.com\/our-team\.php/gim;
const aboutTeamRegExp = /\/web\/([0-9]+)\/http:\/\/www\.freshbooks\.com\/about\/team/gim;


function findURLs(contents) {
  return Array.from(contents.match(ourTeamRegExp) || []).concat(
    contents.match(aboutTeamRegExp)
  );
}

function open(file) {
  const content = fs.readFileSync(file, {encoding: 'utf8'});
  return content;
}

function contentToArray(content) {
  return content.split("\n").filter(_ => _);
}

function writeTo(file, data) {
  const original = fs.readFileSync(file);
  fs.writeFileSync(file, data.join("\n"));
}

function unique(arr) {
    const obj = {};
    for (var i = 0; i < arr.length; i += 1) {
      obj[arr[i]] = true;
    }
    return Object.keys(obj);
};
