using System.Collections.Generic;

namespace dotnet_NEM
{
    public partial class NEMRequest
    {
        public NEMRequest()
        {
            TimeScale = new List<string>{"30MIN"};
        }
        public List<string> TimeScale { get; set; }
    }

}