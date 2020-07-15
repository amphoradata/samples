using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using AmphoraData.Client;
using AutoMapper;
using Humanizer;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

namespace dotnet_NEM
{
    public class Engine
    {
        public static HttpClient HttpClient = new HttpClient();
        private readonly EngineConfig settings;
        private readonly ILogger log;
        private IMapper mapper;

        public Engine(EngineConfig settings, ILogger log)
        {
            settings.ThrowIfInvalid();
            // we're using AutoMapper to transform the data
            var config = new MapperConfiguration(cfg =>
            {
                cfg.CreateMap<Point, CommonData>()
                    .ForMember(m => m.Price, s => s.MapFrom(p => p.Rrp))
                    .ForMember(m => m.ScheduledGeneration, s => s.MapFrom(p => p.Scheduledgeneration))
                    .ForMember(m => m.T, s => s.MapFrom(p => p.SettlementDateUtc()));

                cfg.CreateMap<Point, Actuals>()
                    .IncludeBase<Point, CommonData>()
                    .ForMember(m => m.TotalDemand, s => s.MapFrom(p => p.Totaldemand))
                    .ForMember(m => m.NetInterchange, s => s.MapFrom(p => p.Netinterchange));


                cfg.CreateMap<Point, Forecasts>()
                    .IncludeBase<Point, CommonData>()
                    .ForMember(_ => _.Horizon, o => o.Ignore());

            });
            this.mapper = config.CreateMapper();
            this.settings = settings;
            this.log = log;
        }
        public async Task<RunSummary> Run()
        {
            // create a client for interacting with the NEM API
            var nemClient = new NEMClient();
            var data = await nemClient.Get5MinDataAsync();
            var authClient = new AuthenticationClient(HttpClient);
            authClient.BaseUrl = settings.BaseUrl;
            var token = await authClient.RequestTokenAsync("0", new LoginRequest { Username = settings.UserName, Password = settings.Password });

            token = token.Trim('\"'); // there may be extra quotes on that string
            HttpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

            try
            {
                var signalsClient = new AmphoraeSignalsClient(HttpClient);
                signalsClient.BaseUrl = settings.BaseUrl;
                var actualsMap = Mapping.Actuals; // load the Maps
                var forecastsMap = Mapping.Forecasts;

                // run in parallel for performance
                // ACTUALS
                var nswActualsTask = Task.Run(() => UploadActualAsync(Region.Nsw1,
                    data.Data,
                    signalsClient, actualsMap));
                var vicActualsTask = Task.Run(() => UploadActualAsync(Region.Vic1,
                    data.Data,
                    signalsClient, actualsMap));
                var qldActualsTask = Task.Run(() => UploadActualAsync(Region.Qld1,
                    data.Data,
                    signalsClient, actualsMap));
                var saActualsTask = Task.Run(() => UploadActualAsync(Region.Sa1,
                    data.Data,
                    signalsClient, actualsMap));
                var tasActualsTask = Task.Run(() => UploadActualAsync(Region.Tas1,
                    data.Data,
                    signalsClient, actualsMap));

                // FORECASTS
                var nswForecastsTask = Task.Run(() => UploadForecastsAsync(Region.Nsw1,
                    data.Data,
                    signalsClient, forecastsMap));
                var vicForecastsTask = Task.Run(() => UploadForecastsAsync(Region.Vic1,
                    data.Data,
                    signalsClient, forecastsMap));
                var qldForecastsTask = Task.Run(() => UploadForecastsAsync(Region.Qld1,
                    data.Data,
                    signalsClient, forecastsMap));
                var saForecastsTask = Task.Run(() => UploadForecastsAsync(Region.Sa1,
                    data.Data,
                    signalsClient, forecastsMap));
                var tasForecastsTask = Task.Run(() => UploadForecastsAsync(Region.Tas1,
                    data.Data,
                    signalsClient, forecastsMap));

                var results = await Task.WhenAll(nswActualsTask,
                                                vicActualsTask,
                                                qldActualsTask,
                                                saActualsTask,
                                                tasActualsTask,
                                                nswForecastsTask,
                                                vicForecastsTask,
                                                qldForecastsTask,
                                                saForecastsTask,
                                                tasForecastsTask);
                return new RunSummary(results.ToList());
            }
            catch (ApiException ex)
            {
                log.LogError($"Engine Failed, Message: {ex.Message} ", ex);
                throw ex;
            }
        }


        private async Task<UploadSummary> UploadActualAsync(Region r,
                                              IEnumerable<Point> allPoints,
                                              AmphoraeSignalsClient signalsClient,
                                              System.Collections.Generic.Dictionary<Region, string> map)
        {
            // do a filter here on the points for the region and period type
            var points = allPoints.Where(p => p.Periodtype == Periodtype.Actual && p.Region == r);
            log.LogTrace($"First Point: {JsonConvert.SerializeObject(points.FirstOrDefault())}");
            var batch = new List<Dictionary<string, object>>();
            foreach (var p in points)
            {
                var s = mapper.Map<Actuals>(p);
                batch.Add(s.ToDictionary());
            }
            var id = map[r];
            log.LogInformation($"Using Amphora {id} for region actuals {Enum.GetName(typeof(Region), r)}");
            await signalsClient.UploadSignalBatchAsync(id, "0", batch);
            return new UploadSummary("Actual", r.Humanize(), batch);
        }

        private async Task<UploadSummary> UploadForecastsAsync(Region r,
                                              IEnumerable<Point> allPoints,
                                              AmphoraeSignalsClient signalsClient,
                                              System.Collections.Generic.Dictionary<Region, string> map)
        {
            var points = allPoints.Where(p => p.Periodtype == Periodtype.Forecast && p.Region == r).ToList();
            log.LogTrace($"First Point in forecasts: {JsonConvert.SerializeObject(points.FirstOrDefault())}");

            var batch = new List<Dictionary<string, object>>();
            // first, need to split points into each horizon bin
            // there is only 1 point per horizon
            foreach (var h in Horizon.Horizons)
            {
                if (h.ValueInMinutes.HasValue)
                {
                    var relativePoints = points
                        .Where(p => p.DistanceFromHorizon(h) > -(h.ValueInMinutes / 2))
                        .OrderBy(p => p.DistanceFromHorizon(h)).ToList();

                    var relativePoint = relativePoints.First();
                    // map to amphora model
                    var s = mapper.Map<Forecasts>(relativePoint);
                    s.Horizon = h.Name;

                    // now upload that point
                    batch.Add(s.ToDictionary());
                }
                else
                {
                    // we are doing the max forecast
                    var maxValue = points
                        .OrderBy(p => p.Settlementdate)
                        .Last();

                    var s = mapper.Map<Forecasts>(maxValue);
                    s.Horizon = h.Name;

                    // now upload that point
                    batch.Add(s.ToDictionary());
                }
            }

            var id = map[r];
            log.LogInformation($"Using Amphora {id} for region forecasts {Enum.GetName(typeof(Region), r)}");
            await signalsClient.UploadSignalBatchAsync(id, "0", batch);
            return new UploadSummary("Forecast", r.Humanize(), batch);
        }
    }
}
