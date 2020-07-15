using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Microsoft.Extensions.Configuration;

namespace dotnet_NEM
{
    public static class NEM_http
    {
        // this is a HTTP Trigger for testing locally.
        [FunctionName("NEM_http")] 
        public static async Task<IActionResult> Run(
            [HttpTrigger(AuthorizationLevel.Function, "get", Route = null)] HttpRequest req,
            ILogger log,
            ExecutionContext context)
        {
            var config = new ConfigurationBuilder()
                .SetBasePath(context.FunctionAppDirectory)
                .AddJsonFile("local.settings.json", optional: true, reloadOnChange: true)
                .AddEnvironmentVariables()
                .Build();
            log.LogInformation("C# HTTP trigger function processed a request.");

            var engineConfig = new EngineConfig();
            config.Bind("Amphora", engineConfig);

            var engine = new Engine(engineConfig, log);
            var summary = await engine.Run();

            return new JsonResult(summary);
        }
    }
}

