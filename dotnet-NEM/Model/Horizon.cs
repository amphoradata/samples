using System.Collections.Generic;

namespace dotnet_NEM
{
    public class Horizon
    {
        private const int HOUR = 60;

        public Horizon(string name, int? valueInMinutes)
        {
            Name = name;
            ValueInMinutes = valueInMinutes;
        }

        public string Name { get; set; }
        public int? ValueInMinutes { get; set; }


        public static Horizon FiveMins => new Horizon("5m", 5);
        public static Horizon ThirtyMins => new Horizon("30m", 30);
        public static Horizon ThreeHours => new Horizon("3h", 3 * HOUR);
        public static Horizon SixHours => new Horizon("6h", 6 * HOUR);
        public static Horizon TwelveHours => new Horizon("12h", 12 * HOUR);
        public static Horizon Max => new Horizon("Max", null);

        public static List<Horizon> Horizons => new List<Horizon>
        {
            FiveMins,
            ThirtyMins,
            ThreeHours,
            SixHours,
            TwelveHours,
            Max
        };
    }

}