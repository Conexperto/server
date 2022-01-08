import { Module } from "@nestjs/common";
import { SQLiteClientFactory } from "./shared/infrastructure/persistence/SQLiteClientFactory";


@Module({
	imports: [SQLiteClientFactory],
	controllers: [],
	providers: [],
	exports: []
})
export class BackOfficeModule {}
