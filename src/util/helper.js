const fs = require("fs");
const path = require("path");
const parse = require("csv-parse");

const write = (name, content) => {
  const p = path.resolve(__dirname, `../../public/assets/data/out/${name.age_group}`);
  fs.mkdirSync(p, { recursive: true }, (err) => {
    if (err) throw err;
  });

  let writer = fs.createWriteStream(`${p}/${name.iter}.csv`, {
    flags: "w",
  });
  writer.write(content);
  writer.end();
};

const calculateMedian = (iter = 200, age_group = 8) => {
  let parser = parse({ columns: true, trim: true, cast: true }, function (err, data) {
    for (let j = 0; j < age_group; j++) {
      for (let i = 0; i < iter; i++) {
        // console.log(`Processing age group: ${j}, iteration: ${i}`);

        let res = "Susceptible,Exposed,Hospitalised,Death,Recovered\r\n";

        data
          .filter((f) => f.iter === i && f.age_group === j)
          .forEach((f) => {
            res += `${f.S},${f.E},${f.H},${f.D},${f.R}\r\n`;
          });

        write({ iter: i, age_group: j }, res);
      }
    }
  });

  fs.createReadStream(path.resolve(__dirname, "../../public/assets/output.csv")).pipe(parser);
};

calculateMedian();
