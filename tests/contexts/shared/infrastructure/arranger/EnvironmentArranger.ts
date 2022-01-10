export abstract class EnvironmnetArranger {
	public abstract arrange(): Promise<void>;

	public abstract close(): Promise<void>;
}
