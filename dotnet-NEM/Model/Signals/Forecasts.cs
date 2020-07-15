using System.Collections.Generic;

namespace dotnet_NEM
{
    public class Forecasts : CommonData
    {
        public string Horizon { get; set; }

        public override Dictionary<string, object> ToDictionary()
        {
            return new Dictionary<string, object>(CommonDictionary)
            {
                ["horizon"] = this.Horizon,
            };
        }
    }
}