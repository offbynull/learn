export = viz;
declare class viz {
    constructor(...args: any[]);
    wrapper: any;
    renderImageElement(src: string, ...args: any[]): Promise<any>;
    renderJSONObject(src: string, ...args: any[]): Promise<any>;
    renderSVGElement(src: string, ...args: any[]): Promise<any>;
    renderString(src: string, ...args: any[]): Promise<any>;
}
