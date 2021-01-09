using System;
using System.Collections.Generic;
using System.Text;

namespace ActivityJsonGenerator.Models
{
    public class Activity
    {
        public int Index { get; set; }
        public int Duration { get; set; }
        public List<int> Precedence { get; set; }
        public int[] Resources { get; set; }
    }
}
