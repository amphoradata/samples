using System.Collections.Generic;

namespace dotnet_NEM
{
    // Represents the data we want to put in an Amphora
    public class Actuals : CommonData
    {
        public double TotalDemand { get; set; }
        public double NetInterchange { get; set; }

        public override Dictionary<string, object> ToDictionary()
        {
            return new Dictionary<string, object>(CommonDictionary)
            {
                ["totalDemand"] = this.TotalDemand,
                ["netInterchange"] = this.NetInterchange
            };
        }
    }
}
