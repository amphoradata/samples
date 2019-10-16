using System;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace dotnet_NEM
{
    // This class represents data returned from the NEM API
    public partial class NEMResponse
    {
        [JsonProperty("5MIN")]
        public List<Point> Data { get; set; }
    }

    public partial class Point
    {
        public DateTimeOffset SettlementDateUtc()
        {
            // NEM data is in AEST
            var AEST = TimeZoneInfo.FindSystemTimeZoneById("Australia/Canberra");
            return TimeZoneInfo.ConvertTimeToUtc(Settlementdate, AEST);
        }
        public DateTime Settlementdate { get; set; }
        public Region Regionid { get; set; }

        public Region Region { get; set; }
        public double Rrp { get; set; }
        public double Totaldemand { get; set; }
        public Periodtype Periodtype { get; set; }
        public double Netinterchange { get; set; }
        public double Scheduledgeneration { get; set; }
        public double Semischeduledgeneration { get; set; }
    }

    public enum Periodtype { Actual, Forecast };

    public enum Region { Nsw1, Qld1, Sa1, Tas1, Vic1 };
}   