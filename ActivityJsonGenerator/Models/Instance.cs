using System;
using System.Collections.Generic;
using System.Text;

namespace ActivityJsonGenerator.Models
{
    public class Instance
    {
        public List<Activity> Activities { get; set; }
        public int[] AvailableResources { get; set; }
    }
}
