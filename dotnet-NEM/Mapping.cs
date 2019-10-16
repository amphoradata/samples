using System.Collections.Generic;

namespace dotnet_NEM
{
    public static class Mapping
    {
        // replace the GUIDs below with the ids of the Amphora you made
        public static Dictionary<Region, string> Map => new Dictionary<Region, string>
        {
            [Region.Sa1] = "89c2e30d-78c8-46ef-b591-140edd84ddb6",
            [Region.Nsw1] = "ecc5263e-83b6-42d6-8852-64beffdf204e",
            [Region.Qld1] = "ef22fa0f-010c-4ab1-8a28-a8963f838ce9",
            [Region.Tas1] = "54206ee0-354a-4e7e-946c-69f9c3308635",
            [Region.Vic1] = "3b66da5a-0723-4778-98fc-02d619c70664"
        };
    }
}