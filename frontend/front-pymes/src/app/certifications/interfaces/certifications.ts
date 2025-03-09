export interface certificationsI{
    name: string,
    shortDescription: string;
    progress: number;
    largeDescription: string;
    details: {
        requirements: string;
        benefits: string;
    }
}