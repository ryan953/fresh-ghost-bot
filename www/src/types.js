// @flow

type DateStamp = string;

type Names = Array<string>;

export type TenureType = {
  [key: DateStamp]: {
    additions: number,
    count: number,
    date: DateStamp,
    ghosts: Names,
    newbies: Names,
    removals: number,
    survivors: Names,
  },
};

export type C3 = {
  bindTo?: string,
  data?: Object,
  axis?: Object,
};
