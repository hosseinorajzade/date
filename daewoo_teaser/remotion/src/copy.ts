import type {Run} from './Caption';

// All on-screen copy, exactly as briefed. ZWNJ (U+200C) is kept in words like بی‌صدا.
export const COPY: Record<string, {title: Run[]; desc?: Run[]; size?: number}> = {
  directDrive: {
    title: [{t: 'موتور '}, {t: 'Direct Drive', en: true}],
    desc: [{t: 'عملکرد قدرتمند و بی‌صدا با لرزش کمتر، برای شستشویی آرام‌تر'}],
  },
  modes: {
    title: [{t: '۷ حالت شستشو | '}, {t: '7 Mode', en: true}],
    size: 74,
    desc: [{t: 'برنامه‌ی مناسب برای هر نوع لباس'}],
  },
  energy: {
    title: [{t: 'گرید انرژی '}, {t: 'A+++', en: true}],
    desc: [{t: 'مصرف کمتر برق، صرفه‌جویی بیشتر در هزینه‌ها'}],
  },
  jet: {
    title: [{t: 'Jet Shower', en: true}],
    desc: [{t: 'پاشش قدرتمند آب برای نفوذ عمیق‌تر شوینده در الیاف'}],
  },
  addItem: {
    title: [{t: 'Add Item', en: true}],
    desc: [{t: 'اضافه کردن لباس جامانده در حین شستشو'}],
  },
  capacity: {
    title: [{t: 'ظرفیت '}, {t: '9Kg', en: true}],
    desc: [{t: 'شستشوی حجم بیشتری از لباس‌ها در هر بار'}],
  },
};
