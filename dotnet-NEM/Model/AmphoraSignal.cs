using System.Collections.Generic;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace dotnet_NEM
{
    public class AmphoraSignal
    {
        public System.DateTimeOffset T { get; set; }

        [JsonConverter(typeof(StringEnumConverter))]
        public Periodtype Periodtype { get; set; }

        // numeric below
        public double Price { get; set; }
        public double ScheduledGeneration { get; set; }

        public Dictionary<string, object> ToDictionary()
        {
            return new Dictionary<string, object>
            {
                ["t"] = this.T,
                ["periodType"] = System.Enum.GetName(typeof(Periodtype), this.Periodtype),
                ["price"] = this.Price,
                ["scheduledGeneration"] = this.ScheduledGeneration
            };
        }
    }
}
