using System;
using System.Threading.Tasks;
using Microsoft.Azure.WebJobs;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace dotnet_NEM
{
    public static class ETL_NEM
    {
       [FunctionName("NEM_timer")]
        public static async Task Run([TimerTrigger("0 15,45 * * * *")]TimerInfo myTimer,
                               ILogger log,
                               ExecutionContext context)
        {
            log.LogInformation($"C# Timer trigger function executed at: {DateTime.Now}");

            var config = new ConfigurationBuilder()
                .SetBasePath(context.FunctionAppDirectory)
                .AddJsonFile("local.settings.json", optional: true, reloadOnChange: true)
                .AddEnvironmentVariables()
                .Build();
            log.LogInformation("C# HTTP trigger function processed a request.");

            var engineConfig = new EngineConfig();
            config.Bind("Amphora", engineConfig);

            var engine = new Engine(engineConfig, log);
            await engine.Run();
        }
    }

}
