using System;
using System.Threading.Tasks;
using AmphoraData.Client.Api;
using AmphoraData.Client.Client;
using AmphoraData.Client.Model;
using AutoMapper;
using Microsoft.Extensions.Logging;

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

            // Amphora Dara configuration
            var config = new Configuration()
            {
                BasePath = settings.Host
            };

            var auth = new AuthenticationApi(config);
            var token = await auth.ApiAuthenticationRequestPostAsync(new TokenRequest(settings.UserName, settings.Password));
            token  = token.Trim('\"'); // there may be extra quotes on that string
            config.ApiKey.Add("Authorization", $"Bearer {token}"); // add the token to request headers

            try
            {
                var amphoraApi = new AmphoraeApi(config);
                var map = Mapping.Map; // load the Map

                foreach (var p in data.Data)
                {
                    var s = mapper.Map<AmphoraSignal>(p);
                    var id = map[p.Region];
                    var amphora = amphoraApi.ApiAmphoraeIdGet(id);
                    log.LogInformation($"Using Amphora {amphora.Name}");
                    await amphoraApi.ApiAmphoraeIdSignalsValuesPostAsync(id, s.ToDictionary());
                }
            }
            catch (ApiException ex)
            {
                log.LogError($"Engine Failed, code: {ex.ErrorCode} ", ex);
                throw ex;
            }
        }
    }
}
