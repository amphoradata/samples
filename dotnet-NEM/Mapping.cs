using System.Collections.Generic;

namespace dotnet_NEM
{
    public static class Mapping
    {
        public static Dictionary<Region, string> Map => new Dictionary<Region, string>
        {
            [Region.Nsw1] = "f2e4017e-6fdc-4659-8468-23d0ad423227",
            [Region.Qld1] = "f2e4017e-6fdc-4659-8468-23d0ad423227",
            [Region.Sa1] = "f2e4017e-6fdc-4659-8468-23d0ad423227",
            [Region.Tas1] = "f2e4017e-6fdc-4659-8468-23d0ad423227",
            [Region.Vic1] = "f2e4017e-6fdc-4659-8468-23d0ad423227"
        };
    }
}