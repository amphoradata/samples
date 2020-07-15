using System.Collections.Generic;

namespace dotnet_NEM
{
    public abstract class CommonData
    {
        public abstract Dictionary<string, object> ToDictionary();
        public double Price { get; set; }
        public double ScheduledGeneration { get; set; }
        public System.DateTimeOffset T { get; set; }

        protected Dictionary<string, object> CommonDictionary => new Dictionary<string, object>
        {
            ["t"] = this.T,
            ["price"] = this.Price,
            ["scheduledGeneration"] = this.ScheduledGeneration
        };

    }
}