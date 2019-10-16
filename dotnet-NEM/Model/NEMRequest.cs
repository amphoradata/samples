using System.Collections.Generic;

namespace dotnet_NEM
{
    // This class represents a request made to the NEM API
    public partial class NEMRequest
    {
        public NEMRequest()
        {
            TimeScale = new List<string>{"30MIN"};
        }
        public List<string> TimeScale { get; set; }
    }

}