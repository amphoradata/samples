using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using AmphoraData.Client;
using AutoMapper;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

namespace dotnet_NEM
{
    public class Engine
    {
        private readonly EngineConfig settings;
        private readonly ILogger log;
        private IMapper mapper;

        public Engine(EngineConfig settings, ILogger log)
        {
            settings.ThrowIfInvalid();
            // we're using AutoMapper to transform the data
            var config = new MapperConfiguration(cfg =>
            {
                cfg.CreateMap<Point, AmphoraSignal>()
                .ForMember(m => m.Price, s => s.MapFrom(p => p.Rrp))
                .ForMember(m => m.ScheduledGeneration, s => s.MapFrom(p => p.Scheduledgeneration))
                .ForMember(m => m.T, s => s.MapFrom(p => p.SettlementDateUtc()));

            });
            this.mapper = config.CreateMapper();
            this.settings = settings;
            this.log = log;
        }
        public async Task Run()
        {
            // create a client for interacting with the NEM API
            var nemClient = new NEMClient();
            var data = await nemClient.Get5MinDataAsync();
            var httpClient = new HttpClient();
            var authClient = new AuthenticationClient(httpClient);

            var token = await authClient.RequestTokenAsync("0", new LoginRequest { Username = settings.UserName, Password = settings.Password });

            token = token.Trim('\"'); // there may be extra quotes on that string
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

            try
            {
                var amphoraeClient = new AmphoraeSignalsClient(httpClient);
                amphoraeClient.BaseUrl = settings.Host;
                var map = Mapping.Map; // load the Map
                // run in parallel for performance
                var nswTask = Task.Run(() => UploadPointsAsync(Region.Nsw1, data.Data.Where(d => d.Region == Region.Nsw1), amphoraeClient, map));
                var vicTask = Task.Run(() => UploadPointsAsync(Region.Vic1, data.Data.Where(d => d.Region == Region.Vic1), amphoraeClient, map));
                var qldTask = Task.Run(() => UploadPointsAsync(Region.Qld1, data.Data.Where(d => d.Region == Region.Qld1), amphoraeClient, map));
                var saTask = Task.Run(() => UploadPointsAsync(Region.Sa1, data.Data.Where(d => d.Region == Region.Sa1), amphoraeClient, map));
                var tasTask = Task.Run(() => UploadPointsAsync(Region.Tas1, data.Data.Where(d => d.Region == Region.Tas1), amphoraeClient
                , map));

                await Task.WhenAll(nswTask, vicTask, qldTask, saTask, tasTask);
            }
            catch (ApiException ex)
            {
                log.LogError($"Engine Failed, Message: {ex.Message} ", ex);
                throw ex;
            }
        }


        private async Task UploadPointsAsync(Region r, IEnumerable<Point> points, AmphoraeSignalsClient signalsClient, System.Collections.Generic.Dictionary<Region, string> map)
        {
            log.LogTrace($"First Point: {JsonConvert.SerializeObject(points.FirstOrDefault())}");
            var batch = new List<Dictionary<string, object>>();
            foreach (var p in points)
            {
                var s = mapper.Map<AmphoraSignal>(p);
                batch.Add(s.ToDictionary());
            }
            var id = map[r];
            log.LogInformation($"Using Amphora {id} for region {Enum.GetName(typeof(Region), r)}");
            await signalsClient.UploadSignalBatchAsync(id, "0", batch);
        }
    }
}
