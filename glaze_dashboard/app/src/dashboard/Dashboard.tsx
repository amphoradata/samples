import React from "react";
import moment from "moment";
import {
  SignalsChart,
  EnsurePurchased,
} from "react-amphora";
import { Signal } from "amphoradata";
import { ChartRange } from "react-amphora/dist/components/tsi/ChartRange";

const observationRange: ChartRange = {
  from: moment().startOf("month").toDate(),
  to: moment().toDate(),
};
const forecastRange: ChartRange = {
  from: moment().toDate(),
  to: moment().endOf("week").toDate(),
};

const data = {
  weather: {
    observations: {
      airport: {
        title: "Weather Observations @ Albury Airport",
        amphoraId: "8abb5605-3f7a-419e-bb8f-b4791b6d6534",
        range: observationRange,
        signals: [
          { property: "airTemp" },
          { property: "pressure" },
          { property: "dewPoint" },
          { property: "windSpeed" },
        ],
      },
    },
    forecasts: {
      albury: {
        amphoraId: "57d6593f-1889-410a-b1fb-631b6f9c9c85",
        title: "Weather Forecasts @ Albury",
        range: forecastRange,
        signals: [
          { property: "temperature" },
          { property: "rainfallRate" },
          { property: "rainProb" },
          { property: "pressure" },
        ],
      },
    },
  },
};

interface SectionProps {
  amphoraId: string;
  title: string;
  range: ChartRange;
  signals?: Signal[];
}

const sectionStyle: React.CSSProperties = {};

const ChartSection: React.FC<SectionProps> = (props) => {
  return (
    <div style={sectionStyle} className="card">
      <h4>{props.title}</h4>
      <EnsurePurchased
        amphoraId={props.amphoraId}
        defaultCanReadContents={false}
        defaultCanPurchase={true}
      >
        <SignalsChart
          noAnimate={true}
          range={props.range}
          legend="hidden"
          amphoraId={props.amphoraId}
          signals={props.signals}
        />
      </EnsurePurchased>
    </div>
  );
};

export const Dashboard: React.FC = () => {
  return (
    <div className="container">
      <div className="row">
        <div className="col">
          <ChartSection {...data.weather.observations.airport} />
        </div>
        <div className="col">
          <ChartSection {...data.weather.forecasts.albury} />
        </div>
      </div>
      <hr />
     
    </div>
  );
};
