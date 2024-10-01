import React, { useState, useEffect, useCallback } from "react";
import "./App.css";
import { Flipper, Flipped } from "react-flip-toolkit";
import alSeedData from "../data/allongseeddata.json";
import nlSeedData from "../data/nllongseeddata.json";
import images from "../images";

const Seed = ({ id, team }) => (
  <div className="seed">
    <p>
      {id === 1
        ? "1st"
        : id === 2
        ? "2nd"
        : id === 3
        ? "3rd"
        : id === 4
        ? "WC"
        : id === 5
        ? "WC"
        : id === 6
        ? "WC"
        : id === 7
        ? "Out"
        : id === 8
        ? "Out"
        : null}
    </p>
    <Flipped key={id} flipId={team} stagger={false}>
      <div>
        <img src={images[team]} title={team} alt={team} />
      </div>
    </Flipped>
  </div>
);

function App() {
  const [day, setDay] = useState(0);
  const [alSeeds, setAlSeeds] = useState(alSeedData[day].seeds);
  const [nlSeeds, setNlSeeds] = useState(nlSeedData[day].seeds);
  const [playing, setPlaying] = useState(false);
  const [animate, setAnimate] = useState(null);
  // const [delay, setDelay] = useState(550);

  const getHue = useCallback((_day) => {
    const startingHue = 125;
    const endingHue = 5;
    const hue =
      startingHue -
      Math.ceil((_day * Math.abs(startingHue - endingHue)) / alSeedData.length);
    return hue;
  }, []);

  const timingFunction = useCallback((_day) => {
    const progression = _day / alSeedData.length;
    const fastestMS = 350;
    const slowestMS = 500;
    // x^4: https://www.desmos.com/calculator/fsbzksvytf
    return (
      (slowestMS - fastestMS) * (16 * Math.pow(progression - 0.5, 4)) +
      fastestMS
    );
  }, []);

  // update seeds and tracker
  useEffect(() => {
    setAlSeeds(alSeedData[day].seeds);
    setNlSeeds(nlSeedData[day].seeds);

    const tracker = document.getElementById("progress-tracker");
    tracker.style.width = `${Math.ceil((100 * day) / alSeedData.length)}%`;
    const hue = getHue(day);
    tracker.style.backgroundColor = `hsl(${hue}, 70%, 37%)`;
  }, [day, getHue]);

  // animate seeds and date
  useEffect(() => {
    if (day < alSeedData.length - 1 && playing) {
      const animate = setTimeout(() => {
        setAlSeeds(alSeedData[day].seeds);
        setNlSeeds(nlSeedData[day].seeds);
        setDay(day + 1);
      }, timingFunction(day));
      setAnimate(animate);
    } else {
      setPlaying(false);
    }

    return () => {
      if (animate) clearTimeout(animate);
    };
    // eslint-disable-next-line
  }, [day, playing, timingFunction]);

  useEffect(() => {
    if (!playing) clearTimeout(animate);
    // eslint-disable-next-line
  }, [playing]);

  return (
    <div id="main-container">
      <h1>2024 Post-Season Seeds</h1>
      <div id="progress-container">
        <div id="progress-tracker"></div>
      </div>
      <h2>{alSeedData[day].date}</h2>
      <div>
        <div className="league-column">
          <h3>A.L.</h3>
          <Flipper flipKey={alSeeds.join("")} spring="stiff">
            {alSeeds.map((team, i) => (
              <Seed key={i} id={i + 1} team={team} />
            ))}
          </Flipper>
        </div>
        <div className="league-column">
          <h3>N.L.</h3>
          <Flipper flipKey={nlSeeds.join("")} spring="stiff">
            {nlSeeds.map((team, i) => (
              <Seed key={i} id={i + 1} team={team} />
            ))}
          </Flipper>
        </div>
      </div>
      <div id="source">
        <a href="https://kroljs.com" target="_blank" rel="noreferrer noopener">
          kroljs.com/mlb-seeds-2024
        </a>
      </div>
      <div id="control-panel">
        <input
          type="button"
          onClick={() => {
            setPlaying(false);
            setDay(0);
          }}
          value="FIRST"
        />
        <input
          type="button"
          onClick={() => (day > 0 ? setDay(day - 1) : null)}
          value="PREV"
        />
        <input
          type="button"
          onClick={() => setPlaying(!playing)}
          value={playing ? "PAUSE" : "PLAY"}
        />
        <input
          type="button"
          onClick={() => (day < alSeedData.length - 1 ? setDay(day + 1) : null)}
          value="NEXT"
        />
        <input
          type="button"
          onClick={() => {
            setPlaying(false);
            setDay(alSeedData.length - 1);
          }}
          value="LAST"
        />
      </div>
      <div id="references">
        <span>
          <p>[1]</p>
          <a
            href="https://www.baseball-reference.com/"
            target="_blank"
            rel="noreferrer noopener"
          >
            baseball-reference.com
          </a>
        </span>
        <span>
          <p>[2]</p>
          <a
            href="https://www.sportslogos.net/"
            target="_blank"
            rel="noreferrer noopener"
          >
            sportslogos.net
          </a>
        </span>
        <span>
          <p>[3]</p>
          <a
            href="https://www.mlb.com/news/mlb-playoff-tiebreaker-rules"
            target="_blank"
            rel="noreferrer noopener"
          >
            mlb.com
          </a>
        </span>
      </div>
    </div>
  );
}

export default App;
