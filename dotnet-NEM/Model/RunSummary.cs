using System.Collections.Generic;

namespace dotnet_NEM
{
    public class RunSummary
    {
        public RunSummary(List<UploadSummary> uploaded)
        {
            Uploaded = uploaded;
        }

        public List<UploadSummary> Uploaded { get; set; }
    }
}