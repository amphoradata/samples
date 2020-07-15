using System.Collections.Generic;

namespace dotnet_NEM
{
    public class UploadSummary
    {
        public UploadSummary(string type, string region, List<Dictionary<string, object>> data)
        {
            Type = type;
            Region = region;
            Data = data;
        }

        public string Type { get; set; }
        public string Region { get; set; }
        public List<Dictionary<string, object>> Data { get; set; }
    }
}