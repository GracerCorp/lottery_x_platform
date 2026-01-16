import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Bell, Calendar, Globe } from "lucide-react"
import { SubscribeDialog } from "./subscribe-dialog"

interface LotteryProps {
  name: string
  country: string
  jackpot: string
  nextDraw: string
  frequency: string
  tags?: string[]
}

export function LotteryCard({ name, country, jackpot, nextDraw, frequency, tags }: LotteryProps) {
  return (
    <Card className="hover:shadow-lg transition-shadow duration-300 border-zinc-200 dark:border-zinc-800">
      <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
        <div className="space-y-1">
          <CardTitle className="text-xl font-bold flex items-center gap-2">
            {name}
            <Badge variant="outline" className="text-xs font-normal">
              {country}
            </Badge>
          </CardTitle>
          <div className="text-sm text-muted-foreground flex items-center gap-1">
            <Globe className="h-3 w-3" />
            {currencyForCountry(country)}
          </div>
        </div>
        <div className="bg-primary/10 text-primary rounded-full p-2">
           <span className="text-2xl">💰</span>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div>
            <p className="text-sm font-medium text-muted-foreground">Estimated Jackpot</p>
            <p className="text-3xl font-extrabold text-primary">{jackpot}</p>
          </div>
          
          <div className="flex items-center gap-2 text-sm text-zinc-600 dark:text-zinc-400">
            <Calendar className="h-4 w-4" />
            <span>Next Draw: {new Date(nextDraw).toLocaleDateString()}</span>
          </div>

          <div className="flex flex-wrap gap-2">
             {tags?.map(tag => (
                 <Badge key={tag} variant="secondary" className="text-xs">{tag}</Badge>
             ))}
          </div>
        </div>
      </CardContent>
      <CardFooter className="pt-2">
        <SubscribeDialog lotteryName={name} />
      </CardFooter>
    </Card>
  )
}

function currencyForCountry(country: string) {
    if (country === 'USA') return 'USD';
    if (country === 'Europe') return 'EUR';
    if (country === 'UK') return 'GBP';
    return 'Global';
}
