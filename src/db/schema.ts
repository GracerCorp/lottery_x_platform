import { pgTable, text, timestamp, boolean, jsonb, uuid, integer, primaryKey } from "drizzle-orm/pg-core";
import { type AdapterAccount } from "next-auth/adapters"

export const users = pgTable("user", {
  id: text("id")
    .primaryKey()
    .$defaultFn(() => crypto.randomUUID()),
  name: text("name"),
  email: text("email").notNull(),
  emailVerified: timestamp("emailVerified", { mode: "date" }),
  image: text("image"),
  role: text("role").default("user"),
  createdAt: timestamp("createdAt").defaultNow(),
});

export const accounts = pgTable(
  "account",
  {
    userId: text("userId")
      .notNull()
      .references(() => users.id, { onDelete: "cascade" }),
    type: text("type").$type<AdapterAccount["type"]>().notNull(),
    provider: text("provider").notNull(),
    providerAccountId: text("providerAccountId").notNull(),
    refresh_token: text("refresh_token"),
    access_token: text("access_token"),
    expires_at: integer("expires_at"),
    token_type: text("token_type"),
    scope: text("scope"),
    id_token: text("id_token"),
    session_state: text("session_state"),
  },
  (account) => ({
    compoundKey: primaryKey({
      columns: [account.provider, account.providerAccountId],
    }),
  })
)

export const sessions = pgTable("session", {
  sessionToken: text("sessionToken").primaryKey(),
  userId: text("userId")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  expires: timestamp("expires", { mode: "date" }).notNull(),
})

export const verificationTokens = pgTable(
  "verificationToken",
  {
    identifier: text("identifier").notNull(),
    token: text("token").notNull(),
    expires: timestamp("expires", { mode: "date" }).notNull(),
  },
  (verificationToken) => ({
    compositePk: primaryKey({
      columns: [verificationToken.identifier, verificationToken.token],
    }),
  })
)

// App specific tables

export const lotteries = pgTable("lottery", {
  id: uuid("id").defaultRandom().primaryKey(),
  name: text("name").notNull(), // e.g., Powerball
  slug: text("slug").notNull().unique(), // e.g., powerball-usa
  country: text("country").notNull(), // e.g., USA
  region: text("region"), // e.g., Global, Europe
  frequency: text("frequency"), // e.g., "Wed, Sat"
  logo: text("logo"), // path to image
  description: text("description"), // SEO description
  officialLink: text("officialLink"),
  isActive: boolean("isActive").default(true),
  createdAt: timestamp("createdAt").defaultNow(),
  updatedAt: timestamp("updatedAt").defaultNow(),
});

export const results = pgTable("result", {
  id: uuid("id").defaultRandom().primaryKey(),
  lotteryId: uuid("lotteryId").references(() => lotteries.id).notNull(),
  drawDate: timestamp("drawDate", { mode: "date" }).notNull(),
  numbers: jsonb("numbers").notNull(), // e.g. { main: [1, 2, 3], bonus: [4] }
  jackpot: text("jackpot"), // e.g. "$100 Million"
  currency: text("currency").default("USD"),
  winners: jsonb("winners"), // e.g. [{ tier: 1, prize: 1000000, count: 1 }]
  createdAt: timestamp("createdAt").defaultNow(),
});

export const subscriptions = pgTable("subscription", {
  id: uuid("id").defaultRandom().primaryKey(),
  userId: text("userId").references(() => users.id, { onDelete: "cascade" }).notNull(),
  lotteryId: uuid("lotteryId").references(() => lotteries.id).notNull(),
  notifyEmail: boolean("notifyEmail").default(true),
  notifyPush: boolean("notifyPush").default(false),
  createdAt: timestamp("createdAt").defaultNow(),
});
