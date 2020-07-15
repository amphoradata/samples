using System.Collections.Generic;

namespace dotnet_NEM
{
    public static class Mapping
    {
        // replace the GUIDs below with the ids of the Amphora you made
        public static Dictionary<Region, string> Actuals => new Dictionary<Region, string>
        {
            [Region.Sa1] = "89c2e30d-78c8-46ef-b591-140edd84ddb6",
            [Region.Nsw1] = "ecc5263e-83b6-42d6-8852-64beffdf204e",
            [Region.Qld1] = "ef22fa0f-010c-4ab1-8a28-a8963f838ce9",
            [Region.Tas1] = "54206ee0-354a-4e7e-946c-69f9c3308635",
            [Region.Vic1] = "3b66da5a-0723-4778-98fc-02d619c70664"
        };

        public static Dictionary<Region, string> Forecasts => new Dictionary<Region, string>
        {
            [Region.Sa1] = "c0dd35c9-7bea-4d7d-a476-50bb3574b6c3",
            [Region.Nsw1] = "23055b55-3c39-4b77-ba3d-b708411fb51f",
            [Region.Qld1] = "2c4fe073-7056-4e5c-aeb9-4ac1475f32ca",
            [Region.Tas1] = "a156374d-771c-4f78-8379-87a68b816136",
            [Region.Vic1] = "f877dd24-9d2f-4911-8938-d41ec637642a"
        };
    }
}